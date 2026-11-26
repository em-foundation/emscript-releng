'use strict'

const Path = require('path')
const Fs = require('fs')
const Zip = require('adm-zip')

const DIST_DIR = 'dist'
const TOOLS_DIR = '../../tools'
const TARG_DIR = Path.join(TOOLS_DIR, '@NAME')

const PRE = /^(VERSION)|(LICENSE)/

const PLAT_ARCH = `${process.platform}-${process.arch}`
const ZIP_FILE = Path.join(DIST_DIR, `${PLAT_ARCH}.zip`)

if (!Fs.existsSync(ZIP_FILE)) throw `no support for ${PLAT_ARCH}: can't find ${ZIP_FILE}`

if (Fs.existsSync(TARG_DIR)) Fs.rmSync(TARG_DIR, { recursive: true })
Fs.mkdirSync(TARG_DIR, { recursive: true })

let zip = new Zip(ZIP_FILE)

const root = Path.resolve(TARG_DIR)
const links = zip.getEntries().filter(entry => ((entry.attr >>> 16) & 0xf000) === 0xa000)
const linkFiles = new Set(links.map(entry => Path.resolve(root, entry.entryName)))

const inside = path => {
    const relative = Path.relative(root, path)
    return relative && relative !== '..' && !relative.startsWith('..' + Path.sep) && !Path.isAbsolute(relative)
}

const symlinks = links.map(entry => {
    const path = Path.resolve(root, entry.entryName)
    const link = entry.getData().toString('utf8')
    const target = Path.resolve(Path.dirname(path), link)
    if (!link || Path.isAbsolute(link) || !inside(path) || !inside(target) || linkFiles.has(target)) {
        throw new Error('Invalid package symlink: ' + entry.entryName)
    }
    return { path, link, target }
})

zip.extractAllTo(TARG_DIR, true, true)

// adm-zip extracts link entries as regular files. Restore the relative links after extraction.
symlinks.forEach(({ path, link, target }) => {
    if (!Fs.lstatSync(target).isFile()) throw new Error('Missing library for package symlink: ' + target)
    Fs.unlinkSync(path)
    Fs.symlinkSync(link, path)
})


Fs.readdirSync(DIST_DIR).filter(fn => fn.match(PRE)).forEach(fn => {
    Fs.writeFileSync(Path.join(TARG_DIR, fn), Fs.readFileSync(Path.join(DIST_DIR, fn)))
})

Fs.rmSync(DIST_DIR, { recursive: true })
