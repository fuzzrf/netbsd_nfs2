NetBSD 9.3 remote invalid free

```
nfsrv_create(struct nfsrv_descript *nfsd, struct nfssvc_sock *slp, struct lwp *lwp, struct mbuf **mrq)
{
        struct mbuf *mrep = nfsd->nd_mrep, *md = nfsd->nd_md;
        struct mbuf *nam = nfsd->nd_nam;
        char *dpos = nfsd->nd_dpos;
        kauth_cred_t cred = nfsd->nd_cr;
        struct nfs_fattr *fp;
        struct vattr va, dirfor, diraft;
        struct nfsv2_sattr *sp;
        u_int32_t *tl;
[1]        struct nameidata nd;
        char *cp;
        int32_t t1;
        char *bpos;
        int error = 0, cache = 0, len, tsize, dirfor_ret = 1, diraft_ret = 1;
        int rdev = 0, abort = 0;
        int v3 = (nfsd->nd_flag & ND_NFSV3), how, exclusive_flag = 0;
        char *cp2;
        struct mbuf *mb, *mreq __unused;
        struct vnode *vp = NULL, *dirp = NULL;
        nfsrvfh_t nsfh;
        u_quad_t frev, tempsize;
        u_char cverf[NFSX_V3CREATEVERF];

        nd.ni_cnd.cn_nameiop = 0;
        nfsm_srvmtofh(&nsfh);
[2]        nfsm_srvnamesiz(len);
		...
nfsmout:
        if (dirp)
                vrele(dirp);
        if (abort) {
                VOP_ABORTOP(nd.ni_dvp, &nd.ni_cnd);
                if (nd.ni_dvp == nd.ni_vp)
                        vrele(nd.ni_dvp);
                else
                        vput(nd.ni_dvp);
                if (nd.ni_vp)
                        vput(nd.ni_vp);
        }
        if (nd.ni_pathbuf != NULL) {
[3]                pathbuf_destroy(nd.ni_pathbuf);
                nd.ni_pathbuf = NULL;
        }
        return (error);
}
```

Note that 'nd' struct is not initialized.

If macro on line #2 fails, the code tries to free uninitialized buffer on line #3.

How to repduce:

1. setup nfsd

2. run t1.py


Stack trace:
```
uvm_fault(0xffffb68009351b58, 0xffff900000000000, 2) -> e
[    37.723519] fatal page fault in supervisor mode
[    37.723519] trap type 6 code 0x2 rip 0xffffffff815a6126 cs 0x8 rflags 0x10282 cr2 0xffff900000000000 ilevel 0 rsp 0xffffb68138a59418
[    37.733474] curlwp 0xffffb680093936c0 pid 1117.1057 lowest kstack 0xffffb68138a522c0
[    37.733474] panic: trap
[    37.733474] cpu1: Begin traceback...
[    37.733474] vpanic() at netbsd:vpanic+0x1ee
[    37.743494] panic() at netbsd:panic+0x99
[    37.753503] trap() at netbsd:trap+0x13c8
[    37.753503] --- trap (number 6) ---
[    37.763548] kasan_mark() at netbsd:kasan_mark+0x5e
[    37.773509] pathbuf_destroy() at netbsd:pathbuf_destroy+0x36
[    37.773509] nfsrv_create() at netbsd:nfsrv_create+0xaba
[    37.783510] do_nfssvc() at netbsd:do_nfssvc+0xa4b
[    37.793518] syscall() at netbsd:syscall+0x3b7
[    37.793518] --- syscall (number 155) ---
[    37.793518] netbsd:syscall+0x3b7:
[    37.793518] cpu1: End traceback...

[    37.793518] dumping to dev 168,1 (offset=1039, size=1048446):
[    37.793518] dump Skipping crash dump on recursive panic
[    38.883425] panic: atastart: channel 0 busy, xfer not possible
[    38.883425] cpu1: Begin traceback...
[    38.893423] vpanic() at netbsd:vpanic+0x1ee
[    38.893423] panic() at netbsd:panic+0x99
[    38.903432] atastart() at netbsd:atastart+0x671
[    38.903432] wd_dumpblocks() at netbsd:wd_dumpblocks+0x170
[    38.913435] dk_dump() at netbsd:dk_dump+0x2ae
[    38.913435] dkdump() at netbsd:dkdump+0x1fb
[    38.913435] dump_header_flush() at netbsd:dump_header_flush+0x88
[    38.923426] dump_header_addbytes() at netbsd:dump_header_addbytes+0x40
[    38.923426] dump_header_addseg() at netbsd:dump_header_addseg+0x75
[    38.923426] dump_seg_iter() at netbsd:dump_seg_iter+0x110
[    38.933430] cpu_dump() at netbsd:cpu_dump+0xf0
[    38.933430] dodumpsys() at netbsd:dodumpsys+0x13c
[    38.943431] dumpsys() at netbsd:dumpsys+0x1d
[    38.943431] kern_reboot() at netbsd:kern_reboot+0x7d
[    38.943431] vpanic() at netbsd:vpanic+0x1fd
[    38.953425] panic() at netbsd:panic+0x99
[    38.953425] trap() at netbsd:trap+0x13c8
[    38.963442] --- trap (number 6) ---
[    38.963442] kasan_mark() at netbsd:kasan_mark+0x5e
[    38.983425] pathbuf_destroy() at netbsd:pathbuf_destroy+0x36
[    38.983425] nfsrv_create() at netbsd:nfsrv_create+0xaba
[    38.993430] do_nfssvc() at netbsd:do_nfssvc+0xa4b
[    38.993430] syscall() at netbsd:syscall+0x3b7
[    38.993430] --- syscall (number 155) ---
[    38.993430] netbsd:syscall+0x3b7:
[    38.993430] cpu1: End traceback...

```
